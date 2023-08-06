#ifndef DUNE_POLYGONGRID_ITERATORTAGS_HH
#define DUNE_POLYGONGRID_ITERATORTAGS_HH

#include <iterator>

namespace Dune
{

  namespace __PolygonGrid
  {

    namespace Tag
    {

      // Begin
      // -----

      struct Begin {};



      // End
      // ---

      struct End {};



      namespace
      {

        // begin
        // -----

        const Begin begin = {};



        // end
        // ---

        const End end = {};

      } // anonymous namespace

    } // namespace Tag



    // Envelope
    // --------

    template< class T >
    struct Envelope
    {
      typedef T element_type;
      typedef const T *const_pointer;
      typedef T *pointer;

      template< class... Args >
      explicit Envelope ( Args &&... args )
        : element_( std::forward< Args >( args )... )
      {}

      Envelope ( const Envelope & ) = default;
      Envelope ( Envelope && ) = default;

      Envelope &operator= ( const Envelope & ) = default;
      Envelope &operator= ( Envelope && ) = default;

      explicit operator bool () const noexcept { return true; }

      const typename std::add_lvalue_reference< element_type >::type operator* () const { return element_; }
      typename std::add_lvalue_reference< element_type >::type operator* () { return element_;  }

      const_pointer operator-> () const { return &element_; }
      pointer operator-> () { return &element_; }

    protected:
      element_type element_;
    };




    // VirtualIterator
    // ---------------

    template< class C, class T, class D = std::ptrdiff_t, class R = T >
    using VirtualIterator = std::iterator< C, T, D, Envelope< R >, R >;

  } // namespace __PolygonGrid

} // namespace Dune

#endif // #ifndef DUNE_POLYGONGRID_ITERATORTAGS_HH
